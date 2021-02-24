import * as React from 'react'
import { storiesOf } from '@storybook/react'

import { getSamples } from '../utils/mock'
import { Sample } from '../components/Sample'

storiesOf('components/Sample', module).add('default', () => (
  <Sample title="Sample" samples={getSamples(5)} />
))
