import * as React from 'react'
import { storiesOf } from '@storybook/react'
import { action } from '@storybook/addon-actions'

import { Search } from '../components/Search'

storiesOf('components/Search', module)
  .add('default', () => <Search onChange={action('onChange')} />)
  .add('value', () => (
    <Search value="Custom value" onChange={action('onChange')} />
  ))
