import React from 'react';
import HomeIcon from '@material-ui/icons/Home';
import FastfoodIcon from '@material-ui/icons/Fastfood';
import KitchenIcon from '@material-ui/icons/Kitchen';
import RecipePage from '../main/Recipes/Recipes';
import FridgePage from '../main/Fridge/Fridge';
import HomePage from '../main/Home/Home';

const Routes = [
  {
    path: '/',
    navigationName: 'Home',
    component: HomePage,
    navIcon: <HomeIcon />,
  },
  {
    path: '/camera',
    navigationName: 'Fridge',
    component: FridgePage,
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
