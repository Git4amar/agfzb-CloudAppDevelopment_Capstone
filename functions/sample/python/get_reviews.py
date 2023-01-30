"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core.api_exception import ApiException


def main(params):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        List of reviews
    """
    service = CloudantV1(authenticator=IAMAuthenticator(params["IAM_API_KEY"]))
    service.set_service_url(params["CLOUDANT_URL"])
    try:
        dealership = params["dealerId"]
    except KeyError:
        try:
            response = service.post_all_docs(
                db="reviews", include_docs=True
            ).get_result()
        except ApiException as err:
            print("ERROR", err)
        else:
            return {"body": response["rows"]}
    else:
        try:
            response = service.post_find(
                db="reviews", selector={"dealership": {"$eq": dealership}}
            ).get_result()
        except ApiException as err:
            print("ERROR", err)
        else:
            return {"body": response["docs"]}


# if __name__ == "__main__":
#    main()
