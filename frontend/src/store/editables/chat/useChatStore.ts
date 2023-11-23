// The AIConsole Project
//
// Copyright 2023 10Clouds
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import { create } from 'zustand';

import { ActionSlice, createActionSlice } from './ActionSlice';
import { ChatSlice, createChatSlice } from './ChatSlice';
import { CommandSlice, createCommandSlice } from './CommandSlice';
import { MessageSlice, createMessageSlice } from './MessageSlice';

export type ChatStore = MessageSlice & CommandSlice & ChatSlice & ActionSlice;

export const useChatStore = create<ChatStore>()((...a) => ({
  ...createMessageSlice(...a),
  ...createCommandSlice(...a),
  ...createChatSlice(...a),
  ...createActionSlice(...a),
}));
