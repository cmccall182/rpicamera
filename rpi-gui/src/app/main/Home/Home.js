import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { useSelector } from 'react-redux';
import {
  Typography,
} from '@material-ui/core/';
import { DRAWER_WIDTH, CLOSED_DRAWER_WIDTH } from '../../constants/index';

const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
      width: '25ch',
    },
  },
  shiftContentLeft: {
    marginLeft: CLOSED_DRAWER_WIDTH,
    transition: 'margin-left 450ms cubic-bezier(0.23, 1, 0.32, 1)',
  },
  shiftContentRight: {
    marginLeft: DRAWER_WIDTH,
    transition: 'margin-left 450ms cubic-bezier(0.23, 1, 0.32, 1)',
  },
  content: {
    flexGrow: 1,
    padding: theme.spacing(3),
  },
  recipeInput: {
    width: '25%',
  },
}));

const HomePage = () => {
  const classes = useStyles();
  const open = useSelector(({ navbar }) => navbar.opened);

  return (
    <div>
      <main className={classes.content}>
        <div className={open ? classes.shiftContentRight : classes.shiftContentLeft}>
          <Typography paragraph> Welcome to RPI Fridge Manager</Typography>
        </div>
      </main>
    </div>
  );
};

export default HomePage;
