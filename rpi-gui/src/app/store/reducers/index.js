/* eslint-disable import/no-unresolved */
import { combineReducers } from 'redux';
import navbar from 'app/navigation/store/reducers/navbar.reducer';
import recipe from 'app/main/Recipes/store/reducers/recipes.reducer';

const createReducer = (asyncReducers) => combineReducers({
  navbar,
  recipe,
  ...asyncReducers,
});

export default createReducer;
