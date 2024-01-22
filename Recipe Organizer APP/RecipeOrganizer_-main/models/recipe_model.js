const mongoose = require("mongoose");

const recipeSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
  },
  ingredients: [
    {
      name: { type: String, required: true },
    },
  ],
  instructions: {
    type: String,
    required: true,
  },
  category: {
    type: String,
    enum: ["Breakfast", "Lunch", "Dinner", "Snack", "Dessert", "Other"],
    required: true,
  },
});

const Recipe = mongoose.model("Recipe", recipeSchema);

module.exports = Recipe;
