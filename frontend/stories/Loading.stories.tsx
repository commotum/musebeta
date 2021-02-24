import * as React from 'react'
import { storiesOf } from '@storybook/react'

import { Loading } from '../components/Loading'

storiesOf('components/Loading', module).add('default', () => (
  <Loading title="In progress..." />
))
