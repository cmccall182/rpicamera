import React, { useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { useSelector, useDispatch, connect } from 'react-redux';
import {
  CardMedia, CircularProgress,
} from '@material-ui/core';
import getLatestImage from './store/actions/fridge.actions';
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
  toolbar: theme.mixins.toolbar,
  content: {
    flexGrow: 1,
    padding: theme.spacing(3),
  },
  media: {
    height: 0,
    paddingTop: '56.25%', // 16:9
  },
}));

const FridgePage = (props) => {
  const classes = useStyles();
  const dispatch = useDispatch();
  const open = useSelector(({ navbar }) => navbar.opened);
  const { fridgeData } = props;
  useEffect(() => {
    dispatch(getLatestImage());
  }, []);

  return (
    <div>
      <main className={classes.content}>
        <div className={open ? classes.shiftContentRight : classes.shiftContentLeft}>
          {fridgeData.isFetching ? (
            <CircularProgress />) : (
              <CardMedia
                className={classes.media}
                image={fridgeData.latestImage}
                alt="fridge"
                title="Fridge Status"
              />
          )}
        </div>
      </main>
    </div>
  );
};

const mapStateToProps = (state) => {
  return {
    fridgeData: state.fridgeData,
  };
};

const mapDispatcToProps = (dispatch) => ({
  dispatch,
});

export default connect(mapStateToProps, mapDispatcToProps)(FridgePage);
