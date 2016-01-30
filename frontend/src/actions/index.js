import fetch from 'isomorphic-fetch'
import { fromJS } from 'immutable'

//////////////////////////////////////////////////////////////////////////////
export const REQ_SEARCH = 'REQ_SEARCH'
export const REC_SEARCH = 'REC_SEARCH'

export function reqSearch() {
  return {
    type: REQ_SEARCH
  }
}

export function recSearch(results) {
  return {
    type: REC_SEARCH,
    results
  }
}

export function search(query) {
  return function(dispatch) {
    dispatch(reqSearch())
    return fetch(url)
      .then(data => data.json())
      .then(jsonObj => fromJS(jsonObj))
      .then(results => dispatch(recSearch(results)))
  }
}

//////////////////////////////////////////////////////////////////////////////
export const SELECT_RESULT = 'SELECT_RESULT'

export function selectResult(result) {
  return {
    type: SELECT_RESULT,
    result
  }
}
