import * as React from 'react'
import { storiesOf } from '@storybook/react'
import { action } from '@storybook/addon-actions'

import { TrainModal } from '../components/TrainModal'

storiesOf('modals/TrainModal', module)
  .add('default', () => (
    <TrainModal
      isOpen
      onClose={action('onClose')}
      onStart={action('onStart')}
    />
  ))
  .add('default', () => (
    <TrainModal
      isLoading
      isOpen
      onClose={action('onClose')}
      onStart={action('onStart')}
    />
  ))
