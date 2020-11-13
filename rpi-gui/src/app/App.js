import {
  Switch,
  Route
} from 'react-router-dom';
import { Provider } from 'react-redux';
import Routes from './Routes';
import NavigationBar from './navigation';
import store from './store';
import './App.css';

const App = () => {
  return (
    <Provider store={store}>
    <NavigationBar />
     <Switch>
        {Routes.map((route) => (
          <Route exact path={route.path} key={route.path}>
              <route.component className="content"/>
          </Route>
        ))}
        </Switch>
    </Provider>
  );
}

export default App;