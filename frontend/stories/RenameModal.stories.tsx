import * as React from 'react'
import { storiesOf } from '@storybook/react'
import { action } from '@storybook/addon-actions'

import { RenameModal } from '../components/RenameModal'

storiesOf('modals/RenameModal', module).add('default', () => (
  <RenameModal
    isOpen
    currentName={'OpenAI 774A'}
    onClose={action('onClose')}
    onSubmit={action('onSubmit')}
  />
))
