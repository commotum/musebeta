import * as React from 'react'
import { storiesOf } from '@storybook/react'
import { action } from '@storybook/addon-actions'

import { Model } from '../components/Model'
import { getCheckpoints } from '../utils/mock'

storiesOf('components/Model', module)
  .add('default', () => (
    <Model
      title="Model Name | 04/04/04 | 1000 Steps | training_file.txt"
      checkpoints={getCheckpoints(5)}
      onFork={action('onFork')}
      onGenerate={action('onGenerate')}
    />
  ))
  .add('multiple', () => (
    <>
      <Model
        title="Model Name | 04/04/04 | 1000 Steps | training_file.txt"
        checkpoints={getCheckpoints(5)}
        onFork={action('onFork')}
        onGenerate={action('onGenerate')}
      />
      <Model
        title="Model Name | 04/04/04 | 1000 Steps | training_file.txt"
        checkpoints={getCheckpoints(5)}
        onFork={action('onFork')}
        onGenerate={action('onGenerate')}
      />
    </>
  ))
