import { Record as ImmutableRecord } from 'immutable';

const FridgeData = new ImmutableRecord({
  latestImage: '',
  isFetching: false,
  isFetched: false,
  isError: false,
});

export default FridgeData;
