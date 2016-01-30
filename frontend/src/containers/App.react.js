import React, {
  Component
}
from 'react';

import {
  Link
}
from 'react-router';

class App extends Component {
  render() {
    return (
      <div className="main-app">
      <div className="uk-container uk-container-center">
        <nav className="uk-navbar app-nav">
          <ul className="uk-navbar-nav">
            <li><Link to="/">Paper Search</Link></li>
            <li><Link to="/research-page">ResearchPage</Link></li>
          </ul>
        </nav>
        <hr/>
      <div>
        {this.props.children}
      </div>
      </div>
      </div>
    );
  }
}

export default App;
