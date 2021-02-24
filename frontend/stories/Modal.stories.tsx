import * as React from 'react'
import { storiesOf } from '@storybook/react'
import { action } from '@storybook/addon-actions'

import { Modal } from '../components/Modal'

storiesOf('modals/Modal', module)
  .add('default', () => <Modal isOpen onClose={action('onClose')} />)
  .add('title', () => (
    <Modal title={'Title'} isOpen onClose={action('onClose')} />
  ))
