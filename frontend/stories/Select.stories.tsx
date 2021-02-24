import * as React from 'react'
import { storiesOf } from '@storybook/react'
import { action } from '@storybook/addon-actions'

import { Select } from '../components/Select'

storiesOf('components/Select', module).add('default', () => (
  <Select onChange={action('onChange')} />
))
