import * as React from 'react'
import { storiesOf } from '@storybook/react'
import { action } from '@storybook/addon-actions'

import { DeleteModal } from '../components/DeleteModal'

storiesOf('modals/DeleteModal', module).add('default', () => (
  <DeleteModal
    isOpen
    onClose={action('onClose')}
    onDelete={action('onDelete')}
  />
))
