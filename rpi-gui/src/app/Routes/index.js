import React from 'react';
import HomeIcon from '@material-ui/icons/Home';
import FastfoodIcon from '@material-ui/icons/Fastfood';
import KitchenIcon from '@material-ui/icons/Kitchen';
import RecipePage from '../main/Recipes/Recipes';

const Home = () => {
  return (<div />);
};

const Fridge = () => {
  return (
    <h1>Standings</h1>
  );
};

const Routes = [
  {
    path: '/',
    navigationName: 'Home',
    component: Home,
    navIcon: <HomeIcon />,
  },
  {
    path: '/camera',
    navigationName: 'Fridge',
    component: Fridge,
    navIcon: <KitchenIcon />,
  },
  {
    path: '/recipes',
    navigationName: 'Recipes',
    component: RecipePage,
    navIcon: <FastfoodIcon />,
  },
];

export default Routes;
