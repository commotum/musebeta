import * as React from 'react'
import { storiesOf } from '@storybook/react'

import { TopPanel } from '../components/TopPanel'

storiesOf('components/TopPanel', module)
  .add('default', () => <TopPanel />)
  .add('title', () => <TopPanel title="Hey I am a Title!" />)
