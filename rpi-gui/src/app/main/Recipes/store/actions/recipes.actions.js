import * as Constants from '../../../../constants';

export const getRecipeIngredientsService = async (recipeUrl) => {
  const url = `${Constants.API_URL}/recipes`;
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    body: JSON.stringify(recipeUrl),
  });
  return response;
};

export const getRecipeIngredients = (recipeUrl) => async (dispatch) => {
  try {
    dispatch({ type: Constants.RECIPE_FETCHING });
    const response = await getRecipeIngredientsService(recipeUrl);
    if (!response.ok) {
      dispatch({ type: Constants.RECIPE_ERROR });
    } else {
      dispatch({ type: Constants.RECIPE_FETCHED, payLoad: await response.json() });
    }
  } catch {
    dispatch({ type: Constants.RECIPE_ERROR });
  }
};

export const updateRecipeUrl = (recipeUrl) => (dispatch) => {
  dispatch({ type: Constants.UPDATE_RECIPE_URL, payLoad: recipeUrl });
};
