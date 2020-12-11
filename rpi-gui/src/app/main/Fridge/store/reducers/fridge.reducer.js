import * as Constants from '../../../../constants/index';
import FridgeData from '../records/Record';

const initialState = new FridgeData({});

const reducer = (fridgeData = initialState, action) => {
  switch (action.type) {
    case Constants.FRIDGE_FETCHED:
      return fridgeData.merge({
        isFetched: true,
        isFetching: false,
        latestImage: action?.payLoad,
      });
    case Constants.FRIDGE_FETCHING:
      return fridgeData.merge({ isFetching: true });
    case Constants.FRIDGE_ERROR:
      return fridgeData.merge({ isError: true });
    default:
      return fridgeData;
  }
};

export default reducer;
