CREATE INDEX TagJoinRecipeIdIndex ON TagJoin(RecipeId)
CREATE INDEX TagJoinTagIdIndex ON TagJoin(TagId)

CREATE INDEX ReviewsRecipeIdIndex ON Reviews(RecipeId)
CREATE INDEX ReviewsReviewerIdIndex ON Reviews(ReviewerId)

CREATE INDEX RecipesCreatorIdIndex ON Recipes(CreatorId)