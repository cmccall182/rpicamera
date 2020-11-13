import * as Constants from '../../../constants';

export const toggleNavbar = () => (dispatch) => {
  dispatch({ type: Constants.TOGGLE_NAVBAR });
};
