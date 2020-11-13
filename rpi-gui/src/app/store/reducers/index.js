import { combineReducers } from 'redux';
// eslint-disable-next-line import/no-unresolved
import navbar from 'app/navigation/store/reducers/navbar.reducer';

const createReducer = (asyncReducers) => combineReducers({
  navbar,
  ...asyncReducers,
});

export default createReducer;
