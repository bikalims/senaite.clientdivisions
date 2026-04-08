## senaite.clientdivisions

### Overview

`senaite.clientdivisions` extends **Senaite** (the modern core of Bika LIMS) with 

The Bika Client functionality is cloned as Divisions that live inside their parent Clients. Divisions have full Client functionality, with their own Contacts, Batches, Samples etc. See [Client Divisions](https://www.bikalims.org/new-manual/clients-and-contacts/divisions) in the manual

### Requirements

- **Senaite** (recommended latest version) or **Ingwe Bika LIMS 4**

### Installation

#### Using Buildout (Classic Plone/Senaite)

Add the following to your `buildout.cfg`:

cfg
[buildout]
eggs =
    ...
    senaite.clientdivisions

Then run:
Bashbin/buildout

#### Docker (Recommended for Ingwe Bika LIMS 4)

Add senaite.clientdivisions to your custom add-ons list in the Docker-based Ingwe Bika distribution.

### Manual

[Client Divisions](https://www.bikalims.org/new-manual/clients-and-contacts/divisions)

### License
This project is licensed under the GNU General Public License v2.0 (GPL-2.0).

### Support & Professional Services
[Bika Lab Systems](www.bikalabs.com) offers professional implementation, training, custom development, and support for senaite.clientdivisions.

Website: [https://www.bikalims.org](https://www.bikalims.org)
Email: info@bikalims.org (or contact Lemoene directly)

Made with ❤️ in Cape Town, South Africa
