import * as Constants from '../../../constants';

const initialState = {
  opened: true,
};

const navbar = (state = initialState, action) => {
  switch (action.type) {
    case Constants.TOGGLE_NAVBAR:
      return {
        ...state,
        opened: !state.opened,
      };
    default:
      return state;
  }
};

export default navbar;
