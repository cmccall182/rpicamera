import { Record as ImmutableRecord } from 'immutable';

const RecipeTable = new ImmutableRecord({
  baseIngredients: [],
  neededIngredients: [],
  recipeUrl: '',
  isFetching: false,
  isFetched: false,
  isError: false,
});

export default RecipeTable;
