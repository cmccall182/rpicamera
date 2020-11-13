import { createStore, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';
import logger from 'redux-logger';
import createReducer from './reducers';

const middleware = [thunk, logger];

const store = createStore(createReducer(), applyMiddleware(...middleware));

store.asyncReducers = {};

export default store;
