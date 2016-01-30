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

function searchStore(state = Map({}), action) {
  switch (action.type) {
    default:
    return state
  }
}

const rootReducer = combineReducers({
  searchStore,
  router: routeReducer
});


export default rootReducer
