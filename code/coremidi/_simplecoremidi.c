#include <pthread.h>
#include <mach/mach_time.h>
#include <CoreMIDI/CoreMIDI.h>
#include <CoreFoundation/CoreFoundation.h>
#include <Python.h>

struct module_state {
    PyObject *error;
};

#define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))

struct CMMIDIDestination {
  MIDIEndpointRef  midiDestination;
  CFMutableDataRef receivedMidi;
};

typedef struct CMMIDIDestination* CMMIDIDestinationRef;


static MIDIClientRef _midiClient;


static MIDIClientRef
CMGlobalMIDIClient() {
  if (! _midiClient) {
    MIDIClientCreate(CFSTR("simple core midi client"), NULL, NULL,
                     &(_midiClient));
  }
  return _midiClient;
}

void
CMRecvMIDIProc(const MIDIPacketList* pktList,
                void* readProcRefCon,
                void* srcConnRefCon) {
  CMMIDIDestinationRef destRef = (CMMIDIDestinationRef) readProcRefCon;
  int i;
  const MIDIPacket* pkt;

  pkt = &pktList->packet[0];
  for (i = 0; i < pktList->numPackets; i++) {
    CFDataAppendBytes(destRef->receivedMidi, pkt->data, pkt->length);
    pkt = MIDIPacketNext(pkt);
  }
}

CMMIDIDestinationRef
CMMIDIDestinationCreate(CFStringRef midiDestinationName) {
  CMMIDIDestinationRef destRef
    = CFAllocatorAllocate(NULL, sizeof(struct CMMIDIDestination), 0);
  destRef->receivedMidi = CFDataCreateMutable(NULL, 0);
  MIDIDestinationCreate(CMGlobalMIDIClient(),
                        midiDestinationName,
                        CMRecvMIDIProc,
                        destRef,
                        &(destRef->midiDestination));
  return destRef;
}

void
CMMIDIDestinationDispose(CMMIDIDestinationRef destRef) {
  MIDIEndpointDispose(destRef->midiDestination);
  CFRelease(destRef->receivedMidi);
  CFAllocatorDeallocate(NULL, destRef);
}


static void MIDIEndpoint_Destructor(PyObject* obj) {
  MIDIEndpointRef midiEndpoint = (MIDIEndpointRef)PyCapsule_GetPointer(obj, NULL);
  MIDIEndpointDispose(midiEndpoint);
}


static void MIDIDest_Destructor(PyObject* obj) {
  CMMIDIDestinationRef midiDest = (CMMIDIDestinationRef)PyCapsule_GetPointer(obj, NULL);
  CMMIDIDestinationDispose(midiDest);
}

static PyObject*
CMCreateMIDISource(PyObject* self, PyObject* args) {
  MIDIEndpointRef midiSource;
  CFStringRef midiSourceName;

  midiSourceName =
    CFStringCreateWithCString(NULL, PyUnicode_AsUTF8AndSize(PyTuple_GetItem(args, 0), NULL), kCFStringEncodingUTF8);

  MIDISourceCreate(CMGlobalMIDIClient(), midiSourceName, &midiSource);
  CFRelease(midiSourceName);

  return PyCapsule_New((void*)midiSource, NULL, MIDIEndpoint_Destructor);
}

static PyObject*
CMSendMidi(PyObject* self, PyObject* args) {
  MIDIEndpointRef midiSource;
  PyObject* midiData;
  Py_ssize_t nWords;
  MIDIEventList eventList;
  MIDIEventPacket* pkt;
  UInt32 midiDataToSend[4];
  UInt64 now;
  int i;

  midiSource = (MIDIEndpointRef) PyCapsule_GetPointer(PyTuple_GetItem(args, 0), NULL);
  midiData = PyTuple_GetItem(args, 1);
  nWords = PySequence_Size(midiData);

  for (i = 0; i < nWords; i++) {
    PyObject* midiWord;

    midiWord = PySequence_GetItem(midiData, i);
    midiDataToSend[i] = PyLong_AsLong(midiWord);
  }

  now = mach_absolute_time();
  pkt = MIDIEventListInit(&eventList, kMIDIProtocol_2_0);
  pkt = MIDIEventListAdd(&eventList,
                          sizeof(eventList),
                          pkt,
                          (MIDITimeStamp)now,
                          nWords,
                          midiDataToSend);

  if (pkt == NULL || MIDIReceivedEventList(midiSource, &eventList)) {
    printf("failed to send the midi.\n");
  }

  Py_INCREF(Py_None);
  return Py_None;
}


static PyObject*
CMCreateMIDIDestination(PyObject* self, PyObject* args) {
  CMMIDIDestinationRef destRef;
  CFStringRef midiDestinationName;

  midiDestinationName =
    CFStringCreateWithCString(NULL,
                              PyUnicode_AsUTF8AndSize(PyTuple_GetItem(args, 0), NULL),
                              kCFStringEncodingUTF8);
  destRef = CMMIDIDestinationCreate(midiDestinationName);
  CFRelease(midiDestinationName);
  return PyCapsule_New(destRef, NULL, MIDIDest_Destructor);
}


static PyObject*
CMRecvMidi(PyObject* self, PyObject* args) {
  PyObject* receivedMidiT;
  UInt8* bytePtr;
  int i;
  CFIndex numBytes;
  CMMIDIDestinationRef destRef
    = (CMMIDIDestinationRef) PyCapsule_GetPointer(PyTuple_GetItem(args, 0), NULL);

  numBytes = CFDataGetLength(destRef->receivedMidi);

  receivedMidiT = PyTuple_New(numBytes);
  bytePtr = CFDataGetMutableBytePtr(destRef->receivedMidi);
  for (i = 0; i < numBytes; i++, bytePtr++) {
    PyObject* midiByte = PyLong_FromLong(*bytePtr);
    PyTuple_SetItem(receivedMidiT, i, midiByte);
  }

  CFDataDeleteBytes(destRef->receivedMidi, CFRangeMake(0, numBytes));
  return receivedMidiT;
}

static PyMethodDef SimpleCoreMidiMethods[] = {
  {"send_midi", CMSendMidi, METH_VARARGS, "Send midi data tuple via source."},
  {"recv_midi", CMRecvMidi, METH_VARARGS, "Receive midi data tuple."},
  {"create_source", CMCreateMIDISource, METH_VARARGS, "Create a new MIDI source."},
  {"create_destination", CMCreateMIDIDestination, METH_VARARGS, "Create a new MIDI destination."},
  {NULL, NULL, 0, NULL}
};

static int simplecoremidi_traverse(PyObject* m, visitproc visit, void* arg) {
    Py_VISIT(GETSTATE(m)->error);
    return 0;
}

static int simplecoremidi_clear(PyObject* m) {
    Py_CLEAR(GETSTATE(m)->error);
    return 0;
}

static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "simplecoremidi",
        NULL,
        sizeof(struct module_state),
        SimpleCoreMidiMethods,
        NULL,
        simplecoremidi_traverse,
        simplecoremidi_clear,
        NULL
};

PyObject*
PyInit_simplecoremidi(void)
{
    PyObject* module = PyModule_Create(&moduledef);
    if (module == NULL)
      return NULL;
    struct module_state* st = GETSTATE(module);
    
    st->error = PyErr_NewException("simplecoremidi.Error", NULL, NULL);
    if (st->error == NULL) {
        Py_DECREF(module);
        return NULL;
    }
    return module;
}
