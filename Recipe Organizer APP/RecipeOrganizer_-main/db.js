const { MongoClient } = require("mongodb");
const { ServerApiVersion, ObjectId } = require("mongodb");
const uri =
  "mongodb+srv://heremela:hermela1234@todo.ztqxvqe.mongodb.net/Recipes?retryWrites=true&w=majority";
const client = new MongoClient(uri, {
  serverApi: {
    version: ServerApiVersion.v1,
    strict: true,
    deprecationErrors: true,
  },
});

module.exports = { uri, client };
