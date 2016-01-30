import React from 'react';
import { render } from 'react-dom';
import { Provider } from 'react-redux';
import { compose, createStore, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';

import { createHistory } from 'history';
import useStandardScroll from 'scroll-behavior/lib/useStandardScroll';
import { Router, IndexRoute, Route } from 'react-router';
import { syncHistory, routeReducer } from 'redux-simple-router';
import createLogger from 'redux-logger';

import App from './containers/App.react';
import SearchPage from './containers/SearchPage.react';
import ResearchPage from './containers/ResearchPage.react';
import rootReducer from './reducers/';

const history = useStandardScroll(createHistory)();
const syncHist = syncHistory(history)
const middleware = [syncHist, thunk, createLogger()]

const finalCreateStore = compose(applyMiddleware(...middleware))(createStore)

const store = finalCreateStore(rootReducer)

render(
    <Provider store={store}>
        <Router history={history}>
            <Route path="/" component={App}>
               <IndexRoute component={SearchPage}/>
               <Route path="research-page" component={ResearchPage}/>
            </Route>
        </Router>
    </Provider>,
  document.getElementById('root')
);
