import * as React from 'react'
import { storiesOf } from '@storybook/react'
import { action } from '@storybook/addon-actions'

import { ModalButtons } from '../components/ModalButtons'

storiesOf('components/ModalButtons', module).add('default', () => (
  <ModalButtons
    confirm={{ text: 'Confirm', fn: action('onConfirm') }}
    cancel={{ text: 'Cancel', fn: action('onCancel') }}
  />
))
