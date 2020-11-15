import React, { useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { useSelector, useDispatch, connect } from 'react-redux';
import {
  Button, TextField, CircularProgress, Typography, ListItem, List, ListItemText,
} from '@material-ui/core/';
import { DRAWER_WIDTH, CLOSED_DRAWER_WIDTH } from '../../constants/index';
import recipeActions from './store/actions';

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
}));

const RecipePage = (props) => {
  const classes = useStyles();
  const dispatch = useDispatch();
  const open = useSelector(({ navbar }) => navbar.opened);
  const { recipe } = props;
  useEffect(() => {
    // dispatch(Actions.)
  });

  const handleRecipeSelect = (event) => {
    const { value } = event.target;
    dispatch(recipeActions.updateRecipeUrl(value));
  };

  const handleRecipeSubmit = () => {
    dispatch(recipeActions.getRecipeIngredients(recipe.recipeUrl));
  };

  return (
    <div>
      <main className={classes.content}>
        <div className={open ? classes.shiftContentRight : classes.shiftContentLeft}>
          <div className={classes.toolbar} />
          <form className={classes.root} noValidate autoComplete="off">
            <TextField id="standard-basic" label="Recipe URL" value={recipe.recipeUrl} onChange={(e) => handleRecipeSelect(e)} />
            <Button variant="contained" color="Primary" onClick={handleRecipeSubmit}>Submit</Button>
          </form>
          {!recipe.isError
            && recipe.isFetched
            ? (
              <List>
                {recipe.baseIngredients.map((ingredient) => (
                  <ListItem>
                    <ListItemText primary={ingredient} />
                  </ListItem>
                ))}
              </List>
            ) : (
              <Typography>Error fetching recipe</Typography>
            )}
          {recipe.isFetching && (<CircularProgress />) }
        </div>
      </main>
    </div>
  );
};

const mapStateToProps = (state) => {
  return {
    recipe: state.recipe,
  };
};

const mapDispatcToProps = (dispatch) => ({
  dispatch,
});

export default connect(mapStateToProps, mapDispatcToProps)(RecipePage);
