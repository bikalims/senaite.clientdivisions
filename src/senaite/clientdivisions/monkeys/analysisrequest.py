from bika.lims import api
# from senaite.samplepointlocations import check_installed
# from senaite.samplepointlocations import logger


def get_client_queries(self, obj, record=None):
    """Returns the filter queries to be applied to other fields based on
    both the Client object and record
    """
    # UID of the client
    uid = api.get_uid(obj)
    path = api.get_path(obj)

    # catalog queries for UI field filtering
    queries = {
        "Contact": {
            "getParentUID": [uid, ""]
        },
        "CCContact": {
            "getParentUID": [uid, ""]
        },
        "SamplePoint": {
            "getClientUID": [uid, ""],
        },
        "Template": {
            "getClientUID": [uid, ""],
        },
        "Profiles": {
            "getClientUID": [uid, ""],
        },
        "Specification": {
            "getClientUID": [uid, ""],
        },
        "Sample": {
            "getClientUID": [uid],
        },
        "Batch": {
            "getClientUID": [uid, ""],
        },
        "Division": {
            "path": {
                "query": path,
                "depth": 1
            },
        },
        "PrimaryAnalysisRequest": {
            "getClientUID": [uid, ""],
        }
    }

    # additional filtering by sample type
    record = record if record else {}
    sample_type_uid = record.get("SampleType")
    if api.is_uid(sample_type_uid):
        st_queries = self.get_sampletype_queries(sample_type_uid, record)
        queries.update(st_queries)

    return queries
