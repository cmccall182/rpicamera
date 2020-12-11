import * as Constants from '../../../../constants';

const getLatestImageService = async () => {
  const url = `${Constants.API_URL}/fridge.jpg`;
  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'image/jpg',
      Accept: 'image/jpg',
    },
  });
  return response;
};

const getLatestImage = () => async (dispatch) => {
  dispatch({ type: Constants.FRIDGE_FETCHING });
  const response = await getLatestImageService();
  if (!response.ok) {
    dispatch({ type: Constants.FRIDGE_ERROR });
  } else {
    dispatch({
      type: Constants.FRIDGE_FETCHED,
      payLoad: URL.createObjectURL(await response.blob()),
    });
  }
};

export default getLatestImage;
