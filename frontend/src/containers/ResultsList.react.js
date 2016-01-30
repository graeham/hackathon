import React, {
  Component
}
from 'react';

import Immutable {List, Map} from 'immutable'

class ResultsList extends Component {
  render() {
    return(
      <div>
        Search Page
      </div>
    )
  }
}

ResultsList.propTypes = {
  results: PropTypes.instanceOf(List).isRequired,
  loading: PropTypes.bool.isRequired,
  error: PropTypes.bool.isRequired
}

function mapStateToProps(state) {
  return ({
    results: state.searchStore.get("list"),
    loading: state.searchStore.get("loading"),
    error: state.searchStore.get("error")
  })
}



export default ResultsList
