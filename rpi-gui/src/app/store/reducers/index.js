/* eslint-disable import/no-unresolved */
import { combineReducers } from 'redux';
import navbar from 'app/navigation/store/reducers/navbar.reducer';
import recipe from 'app/main/Recipes/store/reducers/recipes.reducer';
import fridgeData from 'app/main/Fridge/store/reducers/fridge.reducer';

const createReducer = (asyncReducers) => combineReducers({
  navbar,
  recipe,
  fridgeData,
  ...asyncReducers,
});

export default createReducer;
