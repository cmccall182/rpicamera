import React from 'react';
import clsx from 'clsx';
import { makeStyles, useTheme } from '@material-ui/core/styles';
import { NavLink, withRouter } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import Drawer from '@material-ui/core/Drawer';
import Toolbar from '@material-ui/core/Toolbar';
import List from '@material-ui/core/List';
import CssBaseline from '@material-ui/core/CssBaseline';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Typography from '@material-ui/core/Typography';
import AppBar from '@material-ui/core/AppBar';
import Routes from '../Routes';

const drawerWidth = 240;
const closedDrawerWidth = 60;

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
  },
  appBar: {
    padding: theme.spacing(0, 1),
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    height: '5rem',
  },
  appBarShift: {
    marginLeft: drawerWidth - closedDrawerWidth,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  appBarContent: {
    marginLeft: closedDrawerWidth,
  },
  menuButton: {
    marginRight: 0,
  },
  hide: {
    display: 'none',
  },
  drawer: {
    width: drawerWidth,
    flexShrink: 0,
    whiteSpace: 'nowrap',
  },
  drawerOpen: {
    width: drawerWidth,
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  drawerClose: {
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    overflowX: 'hidden',
    width: theme.spacing(7) + 1,
    [theme.breakpoints.up('sm')]: {
      width: theme.spacing(9) + 1,
    },
  },
  toolbar: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: theme.spacing(0, 1),
    // necessary for content to be below app bar
    ...theme.mixins.toolbar,
  },
  content: {
    flexGrow: 1,
    padding: theme.spacing(3),
  },
}));

const NavigationBar = (props) => {
  const dispatch = useDispatch();
  const classes = useStyles();
  const theme = useTheme();
  const open = useSelector(({ navbar }) => navbar.opened);

  const handleDrawerOpen = () => {
    dispatch({ type: 'TOGGLE_NAVBAR' });
  };

  const handleDrawerClose = () => {
    dispatch({ type: 'TOGGLE_NAVBAR' });
  };

  const activeRoute = (routeName) => {
    return props.location.pathname === routeName;
  };

  return (
    <div>
      <CssBaseline />
      <AppBar
        position="sticky"
        className={clsx(classes.appBar, {
          [classes.appBarShift]: open,
        })}
      >
        <Toolbar>
          <Typography className={classes.appBarContent}>
            This is a website
          </Typography>
        </Toolbar>
      </AppBar>
      <Drawer
        variant="permanent"
        className={clsx(classes.drawer, {
          [classes.drawerOpen]: open,
          [classes.drawerClose]: !open,
        })}
        classes={{
          paper: clsx({
            [classes.drawerOpen]: open,
            [classes.drawerClose]: !open,
          }),
        }}
      >
        <div className={classes.toolbar}>
          <IconButton
            className={clsx({
              [classes.hide]: !open,
            })}
            onClick={handleDrawerClose}
          >
            {theme.direction === 'rtl' ? <ChevronRightIcon /> : <ChevronLeftIcon />}
          </IconButton>
          <IconButton
            aria-label="open drawer"
            onClick={handleDrawerOpen}
            edge="start"
            className={clsx(classes.menuButton, {
              [classes.hide]: open,
            })}
          >
            <MenuIcon />
          </IconButton>
        </div>
        <List>
          {Routes.map((route) => (
            <NavLink to={route.path}>
              <ListItem selected={activeRoute(props.path)} key={route.path}>
                <ListItemText primary={route.navigationName} />
              </ListItem>
            </NavLink>
          ))}
        </List>
      </Drawer>
    </div>
  );
};

export default withRouter(NavigationBar);
