import * as React from 'react'
import { storiesOf } from '@storybook/react'
import { action } from '@storybook/addon-actions'

import { Checkpoint } from '../components/Checkpoint'
import { getSamples } from '../utils/mock'
import { Model } from '../components/Model'

storiesOf('components/Checkpoint', module).add('default', () => (
  <Checkpoint
    title="Checkpoint 1"
    samples={getSamples(5)}
    onFork={action('onFork')}
    onGenerate={action('onGenerate')}
  />
))
