const express = require("express");
const ejs = require("ejs");
const bodyParser = require("body-parser");
const mongoose = require("mongoose");
const { MongoClient, ServerApiVersion, ObjectId } = require("mongodb");
const { uri, client } = require("./db");
const PORT = 3000;
const app = express();
const Recipe = require("./models/recipe_model");

app.set("view engine", "ejs");
app.use(express.static("public"));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
//connect to mongodb
try {
  mongoose.connect(uri, { useNewUrlParser: true, useUnifiedTopology: true });

  // Event listener for successful MongoDB connection
  mongoose.connection.on("connected", () => {
    console.log("Connected to MongoDB");
  });

  // Event listener for MongoDB connection error
  mongoose.connection.on("error", (err) => {
    console.error(`MongoDB connection error: ${err}`);
  });
} catch (error) {
  console.error(`Error connecting to MongoDB: ${error}`);
}
///////////////////////////////////////////////////////////////////////////////
app.get("/", (req, res) => {
  res.render("pages/index");
});
app.get("/addrecipe", (req, res) => {
  res.render("pages/addrecipe");
});

//Route to handle fetching Recipes

app.get("/showrecipes", async (req, res) => {
  try {
    const recipes = await client
      .db("Recipes")
      .collection("recipes")
      .find()
      .toArray();

    // Send the recipes as JSON in the response
    res.render("pages/recipes", { recipes: recipes });
  } catch (error) {
    console.error("Error fetching recipes:", error);
    res.status(500).send("Internal Server Error");
  }
});

//////////////////////////////////////////////////////////////////////////////////////////////
app.post("/addrecipe", async (req, res) => {
  const name = req.body.name;
  const ingredients = req.body.ingredients;
  const instructions = req.body.instructions;
  const category = req.body.category;
  const newRecipe = {
    name: name,
    ingredients: ingredients,
    instructions: instructions,
    category: category,
  };
  try {
    // Check if a todo with the same title already exists
    const existingingredient = await client
      .db("Recipes")
      .collection("recipes")
      .findOne({ name: newRecipe.name });

    if (!existingingredient) {
      // If no existing todo, insert the new todo
      await client.db("Recipes").collection("recipes").insertOne(newRecipe);
      console.log("New recipe saved:", newRecipe);
      res.redirect("/showrecipes");
    } else {
      console.log(
        `Recipe with name '${newRecipe.name}' already exists. Skipping insertion.`
      );
      res.send("Recipe already exists. Add another One.");
    }
  } catch (error) {
    console.error("Error saving todo:", error);
    res.status(500).send("Internal Server Error");
  }
});
//////////////////////////////////////////////////////////////////
app.post("/deleterecipe", async (req, res) => {
  const recipeId = req.body.recipeId;
  const recipeObjectId = new ObjectId(recipeId);

  try {
    // Use MongoDB's deleteOne method to remove the todo with the given ID
    const result = await client
      .db("Recipes")
      .collection("recipes")
      .deleteOne({ _id: recipeObjectId });

    if (result.deletedCount === 1) {
      console.log("recipe deleted successfully");
      res.redirect("/showrecipes");
    } else {
      console.log(`recipe with ID ${recipeId} not found`);
    }
  } catch (error) {
    console.error("Error deleting recipe:", error);
    res.status(500).send("Internal Server Error");
  }
});
////////////////////////////////////////////////////////////

app.listen(PORT, () => {
  console.log("server running at port 3000");
});
