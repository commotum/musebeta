import * as React from 'react'
import { storiesOf } from '@storybook/react'
import { action } from '@storybook/addon-actions'
import fetchMock from 'fetch-mock'

import { TrainOptionModal } from '../components/TrainOptionModal'

fetchMock.mock('*', {})

storiesOf('modals/TrainOptionModal', module)
  .add('default', () => (
    <TrainOptionModal
      id=""
      isOpen
      onTrain={action('onTrain')}
      onClose={action('onClose')}
      onContinue={action('onContinue')}
      onNewBranch={action('onNewBranch')}
    />
  ))
  .add('loading', () => (
    <TrainOptionModal
      id=""
      isOpen
      isLoading
      onTrain={action('onTrain')}
      onClose={action('onClose')}
      onContinue={action('onContinue')}
      onNewBranch={action('onNewBranch')}
    />
  ))
