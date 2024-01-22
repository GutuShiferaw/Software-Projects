const { MongoClient } = require("mongodb");
const { ServerApiVersion, ObjectId } = require("mongodb");
const uri =
  "";
const client = new MongoClient(uri, {
  serverApi: {
    version: ServerApiVersion.v1,
    strict: true,
    deprecationErrors: true,
  },
});

module.exports = { uri, client };
