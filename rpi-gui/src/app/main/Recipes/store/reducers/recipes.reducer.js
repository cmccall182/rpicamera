import * as Constants from '../../../../constants/index';
import RecipeTable from '../records/Records';

const initialState = new RecipeTable({});

const reducer = (recipes = initialState, action) => {
  switch (action.type) {
    case Constants.UPDATE_RECIPE_URL:
      return recipes.merge({ recipeUrl: action.payLoad });
    case Constants.RECIPE_FETCHED:
      return recipes.merge({
        isFetched: true,
        isFetching: false,
        baseIngredients: action.payLoad?.recipe,
      });
    case Constants.RECIPE_FETCHING:
      return recipes.merge({ isFetching: true });
    case Constants.RECIPE_ERROR:
      return recipes.merge({ isError: true });
    default:
      return recipes;
  }
};

export default reducer;
