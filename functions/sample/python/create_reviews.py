"""IBM Cloud Function that creates reviews for a dealership

Returns:
    List: Info of created review
"""
from ibmcloudant.cloudant_v1 import CloudantV1, Document
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core.api_exception import ApiException


def main(params):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        Info of created review
    """
    service = CloudantV1(authenticator=IAMAuthenticator(params["IAM_API_KEY"]))

    service.set_service_url(params["CLOUDANT_URL"])

    document = Document.from_dict(params["review"])

    try:
        response = service.post_document(db="reviews", document=document).get_result()
    except ApiException as err:
        print("ERROR", err)
    else:
        return {"body": response}


#if __name__ == "__main__":
#    main()
