import {
  combineReducers
}
from 'redux';

import Immutable, {
  Map, List, Set, fromJS
}
from 'immutable';

import {
  routeReducer
}
from 'redux-simple-router';

import * as Actions from '../actions';

function searchStore(state = Map({
  results: List([]),
  loading: false,
  error: false
}), action) {
  switch (action.type) {
    default:
    return state
  }
}

function researchStore(state = Map({}), action) {
  switch (action.type) {
    default:
    return state
  }
}

const rootReducer = combineReducers({
  searchStore,
  researchStore,
  router: routeReducer
});


export default rootReducer
