import React from 'react';
// import Typography from '@material-ui/core/Typography';

const Home = () => {
  return (<div />);
};

const Fridge = () => {
  return (
    <h1>Standings</h1>
  );
};

const Recipes = () => {
  return (
    <h1>Teams</h1>
  );
};

const Routes = [
  {
    path: '/',
    navigationName: 'Home',
    component: Home,
  },
  {
    path: '/camera',
    navigationName: 'Fridge',
    component: Fridge,
  },
  {
    path: '/recipes',
    navigationName: 'Recipes',
    component: Recipes,
  },
];

export default Routes;
