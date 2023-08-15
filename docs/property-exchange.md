# What is Property Exchange in MIDI 2.0?

Let's say you have a **MIDI 2.0 Capable Device**, meaning the device communicates using MIDI Capability Inquiry (MIDI-CI) and UMPs (Univerisal MIDI Packets). Read my MIDI-CI and UMP blog posts to learn about the base requirements for a MIDI 2.0 device. Using MIDI-CI, MIDI 2.0 devices can request and receieve information about properties of other MIDI 2.0 devices in their network.

Property Exchange is used to Discover, Get, and Set properties of MIDI 2.0 devices such as device configurations, list of controllers, list of programs, and other metadata. Property Exchange provides generalized access to device properties which can enable devices to auto map controllers, change states, provide visual information about a device, and more without special software.

Property Exchange can be supported by devices using both MIDI 1.0, MIDI 2.0, and any other protocols supported by MIDI-CI.

# What steps are required to use Property Exchange.

After a MIDI-CI Discovery Transaction, the MIDI devices will have exchanged their MUIDs, Capabilities (support Profiles and/or Property Exchange), Manufacturer SysEx IDs, and Device Information.

## Property Data Exchange Capabilities
After this, an Initiator device can perform an Inquiry of Property Exchange Capabilities. This inquiry request includes which channel the message is sent over, the source and destination MUIDs, and the number of simultaneous property exchange requests supported.

![Property Data Exchange Capabilities Message](img/pe_inquiry.png)

The responder device responds with almost the same message, confirming that it can exchange property exchange messages and its own number of Simultaneous Property Exchange Requests supported.

![Reply Property Data Exchange Capabilities Message](img/reply_pe_1.png)

## Get ResourceList

Then an Initiator device can perform an Inquiry: Get Property Data with the "ResourceList" Resource to obtain the list of resources that the Responder device has that the Initiatior device can request information about.

![Inquiry: Get Property Data Message](img/get_pe.PNG)

The Get Property Data message requires a Request ID, a number from 0 to 127, that is used to associate a reply to the inquiry and allow a device to support simultaneous property exchange requests.

The Get Property Data message also allows for chunking. If a lot of data was requested, it can be sent in multiple chunks each with the same Request ID.

For a Get Property Data Inquiry for the "ResourceList" Resource, the header data is in a JSON format `{"resource": "ResourceList"}` and the Property Data is empty (as currently defined in MIDI-CI, a Get Property Data Inquiry has no Property Data, so the Length of the Property Data should be set to 0).

The responder device responds with a list of resources that the Initiator Device can request using the Get Property Data Message.

![Reply: Get Property Data Message](img/reply_get_pe.png)

The Header Data of a Reply to Get Property will have a status message in JSON format similar to HTTP status messages like `{"status": 200}`.
The Property Data will have a list of resources that the device supports. If the responder device has 3 resources: DeviceInfo, ChannelList, and CMList, the property data will look like
```
[
    {"resource": "DeviceInfo"},
    {"resource": "ChannelList"},
    {"resource": "CMList"}
]
```

Those two inquiries and two replies are the only ones required to support Property Exchange

## Recommended Optional Resources

It is recommended but optional for a device to support an the Get Property Data with the "DeviceInfo" resource and the "ChannelList" resource to get information about the device and a list of channels that the device supports.

### Device Info

An inquiry for DeviceInfo would have Header Data that looks like `{"resource": "DeviceInfo"}`. The Reply would have Header Data with status and the Property Data might look like this

```
{
    "manufacturerId": [125,0,0],
    "manufacturer": "Educational Use",
    "familyId": [0,0],
    "family": "Example Range",
    "modelId": [48,0],
    "model": "Example Pedal",
    "versionId": [0,0,1,0],
    "version": "1.0"
}
```
These are the required fields in response to a DeviceInfo Inquiry. The manufacturerId denotes the SysEx ID. The familyId, modelId, and versionId can group devices however the manufacturer sees fit.

The response to a DeviceInfo Inquiry can also include a `serialNumber` as well as links which show other resources that can be requested or set that affect the overall settings of a device.

The above Property Data could've been expanded to

```
{
    "manufacturerId": [125,0,0],
    "manufacturer": "Educational Use",
    "familyId": [0,0],
    "family": "Example Range",
    "modelId": [48,0],
    "model": "Example Pedal",
    "versionId": [0,0,1,0],
    "version": "1.0"
    "serialNumber": "12345678",
    "links": [
        {"resource": "X-SystemSettings"}
    ]
}
```

### ChannelList

An inquiry for ChannelList would have Header Data that looks like `{"resource": "ChannelList"}`. The Reply would have Header Data with status and the Property Data might look like this 

```
[
    { 
        "title": "Simple Pedal",
        "channel": 1,
        "links": [
            {"resource": "CMList", "resId": "all"} 
        ] 
    } 
]
```

where channel 1 describes a Simple Pedal that can be affected by a CMList resource. The CMList resource can return different things, so there is also a `resId` identifier to select the desired data.

## Get Resources

Based on the list of resources a Responder device, an Initiator device can Get or Set information about a resource from the Responder device using the Get Property Data and Set Property Data messages. 

A back and forth of getting Property Data using different Request IDs and chunking may look like this

![Property Exchange Requests](img/pe_requests.png)

## Subscribing to Resources

An Initiator device can also Subscribe to a resource if a responder declares the resource as subscribable and be notified when that resource changes using the Subscribe Property Data message.

![Property Exchange Subscribe Message](img/pe_subscribe.png)

The Initiator may start a subscription by sending Header data that includes the resource and the command to start `{"command": "start", "resource": "Current Mode"}`. The responder replies to that message with Header data that includes status and a unique subscribeID for the subscription between this Initiator and Responder device `{"status": 200, "subscribeId": "sub32847623"}`. Then when the resource changes, the Responder can send a subscription message with the command of `partial` if some part of the resource changed, or `full` if the entire resource changed. For example Header data could be `{"command": "full", "subscribeId": "sub32847623"}` and the Property data could be `"multichannel"`. The Initiator may end a subscription the device no longer needs the resource to be synced by sending Header data that includes the command to end and the subscribeId `{"command": "end", "subscribeId": "sub32847623"}`

# For More Information about Property Exchange

There are many more optional resources as well as optional property keys defined by the MMA/AMEI that are not covered in this blog post.

Full documentation for Property Exchange for MIDI-CI is available in the MIDI 2.0 specs at https://www.midi.org/specifications/midi-2-0-specifications/property-exchange-specifications
