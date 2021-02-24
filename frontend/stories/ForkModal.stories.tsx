import * as React from 'react'
import { storiesOf } from '@storybook/react'
import { action } from '@storybook/addon-actions'

import { ForkModal } from '../components/ForkModal'

storiesOf('modals/ForkModal', module).add('default', () => (
  <ForkModal
    isOpen
    onClose={action('onClose')}
    onContinue={action('onContinue')}
  />
))
