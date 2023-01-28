/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
      const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
      const cloudant = CloudantV1.newInstance({
          authenticator: authenticator
      });
      cloudant.setServiceUrl(params.CLOUDANT_URL);
      try {
        if (!params.state) {
            let dbDocList = await cloudant.postAllDocs({
                db: 'dealerships',
                includeDocs: true
            });
            return { "body": dbDocList.result.rows };
        }
        else {
            const selector = {
                "$or": [
                    {'state': params.state},
                    {'st': params.state}
                ]
            };
            let dbDocList = await cloudant.postFind({
                db: 'dealerships',
                selector: selector,
            });
            return { "body": dbDocList.result.docs};
        }
      } catch (error) {
          return { error: error.description };
      }
}

