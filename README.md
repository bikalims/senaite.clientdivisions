## senaite.clientdivisions

### Overview

`senaite.clientdivisions` extends **Senaite** (the modern core of Bika LIMS) with 

The Bika Client functionality is cloned as Divisions that live inside their parent Clients. Divisions have full Client functionality, with their own Contacts, Batches, Samples etc. See [Client Divisions](https://www.bikalims.org/new-manual/clients-and-contacts/divisions) in the manual

**Use Case**
Some of the laboratory’s clients operate multiple facilities, or Divisions, under a single parent company. 

Each Division typically submits its own samples and receives its own reports, while sharing common billing and management oversight

Two operational models are supported:
* Both the parent Client and its Divisions submit samples for themselves
* The parent Client acts purely as an administrative centre, with only the Divisions submitting samples
Because of the physical separation between sites, a parent Client does not submit samples on behalf of its Divisions

**How it works in Bika LIMS**
Clients and their Divisions are set up hierarchically - Divisions live inside their parent Clients and have full Client like functionality, e.g. their own Contacts, Batches, Samples, etc.

**Permissions**
Users with access to the parent Client can view data from all related Divisions, but cannot create Batches or Samples on behalf of those Divisions
Contacts belonging to a Division can see only that Division’s data. They cannot view other Divisions or the parent Client

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
