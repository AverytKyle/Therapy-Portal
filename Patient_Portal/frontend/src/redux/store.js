import { 
    legacy_createStore as createStore, 
    combineReducers,
    applyMiddleware 
} from 'redux'; 
import { createLogger } from 'redux-logger';
import sessionReducer from './session';

// Minimal thunk middleware (works like redux-thunk) to allow dispatching functions
const thunk = ({ dispatch, getState }) => (next) => (action) => {
    if (typeof action === 'function') {
        return action(dispatch, getState);
    }
    return next(action);
};

const rootReducer = combineReducers({
    session: sessionReducer,
});

let enhancer;
if (process.env.NODE_ENV === 'production') {
    enhancer = applyMiddleware(thunk);
} else {
    const logger = createLogger({ collapsed: true });
    // Use the browser extension compose if available, otherwise fallback to identity.
    const composeEnhancers = (typeof window !== 'undefined' && window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__) || ((f) => f);
    enhancer = composeEnhancers(applyMiddleware(thunk, logger));
}

const configureStore = (preloadedState) => {
    return createStore(rootReducer, preloadedState, enhancer);
}
export default configureStore;
